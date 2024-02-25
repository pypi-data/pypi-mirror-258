from agentscript_pyo3 import Parser


def test_parse_full_message():
    print("creating parser")
    parser = Parser()

    print("processing message")

    message = 'We need to do translation <Invoke tool="Translator" action="translate" parameters={"text": "Hello", "options": {"from": "en", "to": "es"}} /> with some tailing text'
    parser.parse(message)

    print("processed message")
    parsed_data = parser.get_parsed_data()

    assert len(parsed_data) == 1
    data = parsed_data[0]
    print(f"Tool: {data.tool}, Action: {data.action}")

    parameters = data.get_parameters()
    print(f"Parameters: {parameters}")

    assert data.tool == "Translator"
    assert data.action == "translate"
    assert parameters["text"] == "Hello"
    assert parameters["options"]["from"] == "en"
    assert parameters["options"]["to"] == "es"


def test_parse_partial_message():
    parser = Parser()

    message = 'We need to do translation <Invoke tool="Translator" ac'
    parser.parse(message)

    expect_no_data = parser.get_parsed_data()
    print("partial parsed data: ", expect_no_data)
    assert len(expect_no_data) == 0

    message = 'tion="translate" parameters={"text": "Hello", "options": {"from": "en", "to": "es"}} /> with some tailing text'
    parser.parse(message)
    print("processed message")

    parsed_data = parser.get_parsed_data()

    assert len(parsed_data) == 1
    data = parsed_data[0]
    print(f"Tool: {data.tool}, Action: {data.action}")

    parameters = data.get_parameters()
    print(f"Parameters: {parameters}")

    assert data.tool == "Translator"
    assert data.action == "translate"
    assert parameters["text"] == "Hello"
    assert parameters["options"]["from"] == "en"
    assert parameters["options"]["to"] == "es"

    message = 'We need to do translation <Invoke tool="Translator" action="translate" parameters={"text": "Hello", "options": {"from": "en", "to": "es"}} />'
    parser.parse(message)

    parsed_data = parser.get_parsed_data()
    print("final process: ", parsed_data)
    assert len(parsed_data) == 2


if __name__ == "__main__":
    test_parse_full_message()
    test_parse_partial_message()
