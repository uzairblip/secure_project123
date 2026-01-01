import requests
import sys

# The URL of your local server
BASE_URL = "http://127.0.0.1:8000"
# Path to your custom login view
LOGIN_URL = f"{BASE_URL}/inventory/login/" 

def print_header(text):
    print(f"\n{'='*60}")
    print(f"🛡️  {text}")
    print(f"{'='*60}")

def test_xss_protection():
    print_header("TESTING: XSS PAYLOAD SANITIZATION")
    xss_payload = "<script>alert('HACKED')</script>"
    print(f"🚀 Injecting Payload into Username Field: {xss_payload}")
    
    # We use a session to mimic a browser
    session = requests.Session()
    
    # First, get the page to receive the CSRF cookie
    session.get(LOGIN_URL)
    csrftoken = session.cookies.get('csrftoken', '')

    payload = {
        'username': xss_payload, 
        'password': 'any_password',
        'csrfmiddlewaretoken': csrftoken,
        'captcha_0': 'dummy',
        'captcha_1': 'wrong'
    }
    
    response = session.post(LOGIN_URL, data=payload, headers={'Referer': LOGIN_URL})
    
    # Check if the script tag is rendered raw (Dangerous) or escaped (Safe)
    if xss_payload in response.text and "<script>" in response.text:
         print("❌ FAIL: Vulnerability Found! Script tags are being rendered raw.")
    else:
         print("✅ SUCCESS: XSS Payload was sanitized/escaped by the system.")

def test_brute_force_lockout():
    print_header("TESTING: ACCOUNT LOCKOUT (3-STRIKE POLICY)")
    username = "admin"  # We will target this user for the lockout test
    
    session = requests.Session()

    # We try 5 attempts to be absolutely sure we hit the threshold of 3
    for i in range(1, 6):
        print(f"🔄 Attempt {i}: Sending malicious login request...")
        
        # Refresh CSRF for each attempt
        session.get(LOGIN_URL)
        csrftoken = session.cookies.get('csrftoken', '')

        payload = {
            'username': username,
            'password': 'wrong_password_test',
            'csrfmiddlewaretoken': csrftoken,
            'captcha_0': 'dummy', 
            'captcha_1': 'wrong'
        }
        
        # allow_redirects=True ensures we see the final page after the lockout redirect
        response = session.post(LOGIN_URL, data=payload, headers={'Referer': LOGIN_URL}, allow_redirects=True)
        
        # 🛡️ Look for keywords indicating the lockout triggered
        content = response.text.lower()
        if "locked" in content or "multiple failures" in content or "15 minutes" in content:
            print(f"✅ SUCCESS: System detected attack. Attempt {i} was BLOCKED by Lockout Policy.")
            return
        else:
            print(f"ℹ️ Attempt {i}: Standard rejection (System still open).")
    
    print("❌ FAIL: System did not lock the account after 5 attempts.")

if __name__ == "__main__":
    print("\n🚀 STARTING AUTOMATED DEVSECOPS SECURITY AUDIT")
    print(f"Targeting: {BASE_URL}")
    
    try:
        # Test 1: XSS (Cross-Site Scripting)
        test_xss_protection()
        
        # Test 2: Brute Force & Lockout
        test_brute_force_lockout()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Server is not running! Run 'python manage.py runserver' first.")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
    
    print("\n🏁 AUDIT COMPLETE")