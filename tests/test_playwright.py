import pytest
from playwright.sync_api import sync_playwright, Page, expect

@pytest.fixture(scope="function")
def browser():
    """Launches a browser for each test case."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200) 
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


def test_simple_form_demo(browser: Page):
    """Tests the 'Simple Form Demo' page."""
    browser.goto("https://www.lambdatest.com/selenium-playground")
    browser.wait_for_selector("text=Simple Form Demo")
    browser.get_by_text("Simple Form Demo").click()

    expect(browser).to_have_url("https://www.lambdatest.com/selenium-playground/simple-form-demo")

    input_locator = browser.get_by_placeholder("Please enter your Message")
    browser.wait_for_selector("input[placeholder='Please enter your Message']")

    input_locator.click()

    message = "Welcome to LambdaTest"
    input_locator.type(message, delay=100) 

    expect(input_locator).to_have_value(message, timeout=5000)

    button_locator = browser.get_by_role("button", name="Get Checked Value")
    browser.wait_for_selector("button:has-text('Get Checked Value')")

    browser.wait_for_timeout(1000)

    button_locator.click()

    browser.wait_for_selector("#message", state="visible", timeout=15000)
    expect(browser.locator("#message")).to_contain_text(message, timeout=10000)
 
  
def test_drag_and_drop_sliders(browser: Page):
    """Tests the Drag & Drop slider functionality for 'Default value 15' slider."""
    
    browser.goto("https://www.lambdatest.com/selenium-playground")
    browser.get_by_text("Drag & Drop Sliders").click()

    # Locate the slider with default value 15 (using class selector)
    slider = browser.locator('input[type="range"].sp__range[value="15"]')
    expect(slider).to_be_visible()

    # Locate the specific output element associated with this slider
    value_display = slider.locator('xpath=following-sibling::output')

    # Get the slider position and bounds
    box = slider.bounding_box()
    assert box is not None, "Slider bounding box not found"

    # Calculate the target position for the value 95
    target_value = 95
    slider_range = 100 - 1  # max - min
    slider_position = (target_value - 1) / slider_range * box["width"]

    # Fine-tune the position if needed (small adjustment to prevent overshooting)
    slider_position -= 10  

    # Move the slider using the mouse 
    browser.mouse.move(box["x"] + slider_position, box["y"] + box["height"] / 2)
    browser.mouse.down()
    browser.mouse.move(box["x"] + slider_position, box["y"] + box["height"] / 2)
    browser.mouse.up()

    # check if the value is updated 
    expect(value_display).to_have_text("95", timeout=5000)

    actual_value = value_display.text_content()
    assert actual_value == "95", f"Expected slider value to be 95, but got {actual_value}"

def test_input_form_submit(browser: Page):
    """Tests form submission with validation messages in Playwright."""
    # Step 1: Open the page and click "Input Form Submit"
    browser.goto("https://www.lambdatest.com/selenium-playground")
    browser.get_by_text("Input Form Submit").click()

    # Step 2: Click "Submit" without filling in any information in the form
    submit_button = browser.get_by_role("button", name="Submit")
    submit_button.click()

    # Step 3: Assert "Please fill out this field." error message
    error_messages = browser.locator("input:invalid")

    # Ensure at least one invalid field exists
    expect(error_messages).not_to_have_count(0, timeout=5000)

    # total number of invalid fields matches expected
    expect(error_messages).to_have_count(14, timeout=5000)
    
    browser.get_by_placeholder("Name").first.type("Test Lambda")
    browser.locator('#inputEmail4').type("Test@gmail.com")
    browser.get_by_placeholder("Password").first.type("Test_Lambda#@123")
    browser.get_by_placeholder("Company").first.type("LambdaTest ITS")
    browser.get_by_placeholder("Website").first.type("www.lambdatest.com")
    browser.get_by_placeholder("City").first.type("ECape town")
    browser.get_by_placeholder("Address 1").first.type("27 Buitekant St.")
    browser.get_by_placeholder("Address 2").first.type("City Bowl")
    browser.get_by_placeholder("State").first.type("Kuvukiland")
    browser.get_by_placeholder("Zip Code").first.type("111111")

    # Step 5: select "United States" from drop down
    browser.locator("#seleniumform select").select_option(label="United States")

    # Step 6: Fill in all fields and "Submit"
    submit_button.click()

    # Step 7: Validate the success message
    expect(browser.get_by_text("Thanks for contacting us, we will get back to you shortly.")).to_be_visible(timeout=5000)
    
if __name__ == "__main__":
    pytest.main(["-v", "--headed"])
