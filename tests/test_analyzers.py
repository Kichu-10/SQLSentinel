from sqlsentinel.analyzers import detect_db_errors, similarity, detect_waf

def test_mysql_error_signature():
    assert "MySQL" in detect_db_errors("You have an error in your SQL syntax")

def test_clean_text_no_errors():
    assert detect_db_errors("Product details loaded successfully") == []

def test_similarity():
    assert similarity("hello world", "hello world") == 1.0
    assert similarity("aaaa", "bbbb") < 1.0

def test_waf_status():
    assert detect_waf(403, "no")
