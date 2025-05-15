from pages.calculator_page import CalculatorPage

def test_addition(driver):
    calc = CalculatorPage(driver)

    calc.click_7()
    calc.click_plus()
    calc.click_9()
    calc.click_equals()

    result = calc.get_result()
    assert result == "16", f"❌ ОШИБКА: ожидалось '16', но получено '{result}'"
