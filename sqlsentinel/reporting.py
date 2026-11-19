import json
from pathlib import Path
from jinja2 import Template

HTML = """<!doctype html><html><head><meta charset="utf-8"><title>SQLSentinel Report</title>
<style>body{font:15px system-ui;max-width:1000px;margin:40px auto;padding:0 18px;color:#18212f}
.card{border:1px solid #d7dee8;border-radius:10px;padding:16px;margin:12px 0}
small{color:#64748b}.medium{border-left:5px solid #d69e36}.high{border-left:5px solid #dc6868}
.info{border-left:5px solid #6398ce}code{overflow-wrap:anywhere}</style></head><body>
<h1>SQLSentinel Audit Report</h1><p><b>Target:</b> <code>{{ r.target }}</code></p>
<p><b>Host:</b> {{ r.host }} · <b>Requests:</b> {{ r.requests_sent }}</p>
<p><small>{{ r.started_at }} to {{ r.completed_at }}</small></p>
<h2>Findings ({{ r.findings|length }})</h2>
{% for f in r.findings %}<section class="card {{ f.severity }}"><h3>{{ f.title }}</h3>
<p><b>{{ f.severity|upper }}</b> · {{ f.category }} · {{ f.confidence }}</p>
{% if f.parameter %}<p>Parameter: <code>{{ f.parameter }}</code></p>{% endif %}
<p>{{ f.evidence }}</p><p><b>Recommendation:</b> {{ f.recommendation }}</p></section>
{% else %}<p>No indicators detected by the enabled checks.</p>{% endfor %}
<h2>Notes</h2><ul>{% for n in r.notes %}<li>{{ n }}</li>{% endfor %}</ul>
<p><small>Indicators require manual validation. This tool does not prove absence or presence of a vulnerability.</small></p>
</body></html>"""

def write_report(report, fmt: str, output: str):
    data = report.model_dump()
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    elif fmt == "html":
        path.write_text(Template(HTML).render(r=report), encoding="utf-8")
    else:
        lines = [f"SQLSentinel report: {report.target}", f"Requests: {report.requests_sent}", ""]
        for f in report.findings:
            lines += [f"[{f.severity.upper()}] {f.title}", f"Evidence: {f.evidence}",
                      f"Recommendation: {f.recommendation}", ""]
        lines += ["Notes:"] + [f"- {n}" for n in report.notes]
        path.write_text("\\n".join(lines), encoding="utf-8")
    return path
