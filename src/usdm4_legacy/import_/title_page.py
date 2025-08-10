from simple_error_log.errors import Errors
from simple_error_log.error_location import KlassMethodLocation
from usdm4_legacy.claude.claude import Claude

class TitlePage():
    def __init__(self, sections: list[str], errors: Errors):
        self._sections = sections
        self._errors = errors
        self._ai = Claude(self._errors)

    def process(self):
        text = ""
        index = 0
        not_numbered = True
        while not_numbered:
            if self._sections[index]['section_number'] != "":
                not_numbered = False
            else:
                text += self._sections[index]['html_content']
            index += 1
        prompt = f"""
            from the html below

            {text}

            Extract the following informatio into a JSON structure , please extract the following information:
            - The title of the clinical trial protocol document
                - PLace into the field "official"
            - The trial phase
                - Place into the field "phase"
            - The NCT number allocated to the study. 
                - The NCT number takes for the format "NCT" followed by 8 digits. 
                - Place into a "ct.gov" field
            - The sponsor's company name 
                - Place into the field "sponsor"
            - The sponsor's study or trial identifier
                - placed into a field "sponsor_identifier"
            - The sponsor's address
                - The address should be split into several fields
                    - The city placed into a "city" field
                    - the zip or postal code placed into a "postalCode" field 
                    - The state or region placed into a "state" field
                    - The country returned in a "country" field as a ISO 3166 country code
                    - Any other infomration returned as lines as an array in a "lines" field
            If no results can be found return an empty JSON structure.
            """
        prompt_result = self._ai.prompt(prompt)
        print(f"TRIAL INFO: {prompt_result}")
        # result = self._extract_result(prompt_result)
        # print(f"TRIAL INFO RESULT: {result}")
        # return result
                