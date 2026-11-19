import time
from datetime import datetime, timezone
from urllib.parse import urlsplit, parse_qsl
from .analyzers import detect_db_errors, detect_waf, similarity
from .http import RequestEngine
from .models import Finding, ScanReport
from .probes import QUOTE_PROBE, TRUE_PROBE, FALSE_PROBE, replace_parameter

class RequestBudgetExceeded(RuntimeError):
    pass

class Scanner:
    def __init__(self, max_requests: int = 12, delay: float = 1.0, timeout: float = 8.0):
        if not 1 <= max_requests <= 50:
            raise ValueError("max_requests must be between 1 and 50.")
        if delay < 0.5:
            raise ValueError("delay must be at least 0.5 seconds.")
        self.max_requests = max_requests
        self.delay = delay
        self.engine = RequestEngine(timeout=timeout)
        self.sent = 0

    def _get(self, url: str):
        if self.sent >= self.max_requests:
            raise RequestBudgetExceeded("Request budget exhausted.")
        if self.sent:
            time.sleep(self.delay)
        self.sent += 1
        return self.engine.get(url)

    def scan(self, url: str, host: str) -> ScanReport:
        report = ScanReport(target=url, host=host)
        try:
            baseline = self._get(url)
            baseline_text = baseline.text[:20000]
            base_errors = detect_db_errors(baseline_text)
            if base_errors:
                report.findings.append(Finding(
                    category="error-disclosure", severity="medium", confidence="medium",
                    title="Database error signature present in baseline",
                    evidence="Database-specific error signature(s): " + ", ".join(base_errors),
                    recommendation="Return generic client errors and log database diagnostics server-side."
                ))
            if detect_waf(baseline.status_code, baseline_text):
                report.notes.append("Baseline response resembles a WAF, access-control, or rate-limit response.")
            params = list(dict.fromkeys(k for k, _ in parse_qsl(urlsplit(url).query, keep_blank_values=True)))
            report.parameters_tested = params
            for parameter in params:
                if self.sent >= self.max_requests:
                    report.notes.append("Stopped at configured request budget.")
                    break
                try:
                    quote_url = replace_parameter(url, parameter, QUOTE_PROBE.value)
                    quote_response = self._get(quote_url)
                    quote_errors = detect_db_errors(quote_response.text[:20000])
                    new_errors = [e for e in quote_errors if e not in base_errors]
                    if new_errors:
                        report.findings.append(Finding(
                            category="error-based-indicator", severity="medium", confidence="medium",
                            parameter=parameter,
                            title="Database error signature triggered by quote probe",
                            evidence="New signature(s): " + ", ".join(new_errors) +
                                     f"; HTTP {quote_response.status_code}.",
                            recommendation="Use parameterized queries and suppress database error details in responses."
                        ))
                except RequestBudgetExceeded:
                    break
                if self.sent + 2 > self.max_requests:
                    report.notes.append(f"Boolean comparison skipped for {parameter}: insufficient request budget.")
                    continue
                try:
                    true_url = replace_parameter(url, parameter, TRUE_PROBE.value)
                    false_url = replace_parameter(url, parameter, FALSE_PROBE.value)
                    true_response = self._get(true_url)
                    false_response = self._get(false_url)
                    score = similarity(true_response.text[:20000], false_response.text[:20000])
                    length_delta = abs(len(true_response.text) - len(false_response.text))
                    if score < 0.88 and length_delta >= 40 and not (
                        detect_waf(true_response.status_code, true_response.text) or
                        detect_waf(false_response.status_code, false_response.text)
                    ):
                        report.findings.append(Finding(
                            category="boolean-response-difference", severity="high", confidence="low-to-medium",
                            parameter=parameter,
                            title="Boolean probes produced materially different responses",
                            evidence=f"Response similarity={score:.3f}; body length delta={length_delta}; "
                                     f"statuses={true_response.status_code}/{false_response.status_code}. "
                                     "Application-specific behavior can cause false positives.",
                            recommendation="Reproduce in an approved test environment and review server-side query parameterization."
                        ))
                except RequestBudgetExceeded:
                    break
            report.notes.append("No database contents were retrieved or modified.")
            report.notes.append("A negative result does not establish that the endpoint is free of SQL injection.")
        finally:
            report.requests_sent = self.sent
            report.completed_at = datetime.now(timezone.utc).isoformat()
            self.engine.close()
        return report
