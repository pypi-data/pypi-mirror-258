import re

class InfoExtractor:
    """
    A class for extracting phone numbers, links, and emails from text.
    """
    PHONE_NUMBER_PATTERNS = [
        r'\(\d{3}\)[ -]?\d{3}[ -]?\d{4}',  # (123) 456-7890 or (123)4567890
        r'\d{3}[.-]?\d{3}[.-]?\d{4}',      # 123-456-7890 or 123.456.7890
        r'\d{10}',                          # 1234567890
        r'\+\d{1}\s?\(\d{3}\)[ -]?\d{3}[ -]?\d{4}',  # +1 (123) 456-7890 or +1(123)4567890
        r'\+?1?[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}',  # +1-123-456-7890 or 1-(123)-456-7890
        r'^(?:\+\d{1}\s?\(\d{3}\)|\d{1,2}[ -]?\(?\d{3}\)?)[ -]?\d{3}[ -]?\d{4}$'  # Example: +1 (555) 123-4567 or 555-123-4567
    ]

    LINK_PATTERNS = [
        r'(?<=\(|\s)https?://[\w./-]+(?=\)|\s|$)',  # Example: http://example.com, https://www.example.org
        r'(?<=\(|\s)www\.[\w./-]+(?=\)|\s|$)',      # Example: www.example.com, www.example.org
        r'(?<=\.)[\w./-]+\.(?:com|org|net|gov|edu|co\.uk|\w{2,})(?=(?:\s|\. |, |\)))',  # Example: example.com, example.co.uk
        r'(?<=\(|\s)[\w-]+\.example\.[\w./-]+(?=\)|\s|$)',  # Example: sub-domain.example.com
        r'http[s]?://\S+',  # Matches any URL starting with http:// or https://
        r'www\.[\w-]+\.\w+',  # Matches www.sub-domain.example.com
        r'[\w.-]+\.(?:com|org|net|gov|edu|co\.uk|\w{2,})(?:\/[\w./?=%&-]*)?',  # Matches example.com/page?query=value
        r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',  # Matches IP addresses
    ]

    EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    @classmethod
    def extract_phone_numbers(cls, text):
        """
        Extract phone numbers from text using predefined patterns.

        Args:
            text (str): The input text containing phone numbers.

        Returns:
            list: A list of extracted phone numbers.
        """
        return cls._extract_using_patterns(text, cls.PHONE_NUMBER_PATTERNS)

    @classmethod
    def extract_links(cls, text):
        """
        Extract links from text using predefined patterns.

        Args:
            text (str): The input text containing links.

        Returns:
            list: A list of extracted links.
        """
        return cls._extract_using_patterns(text, cls.LINK_PATTERNS)

    @classmethod
    def extract_emails(cls, text):
        """
        Extract email addresses from text using a predefined pattern.

        Args:
            text (str): The input text containing email addresses.

        Returns:
            list: A list of extracted email addresses.
        """
        return re.findall(cls.EMAIL_PATTERN, text)

    @classmethod
    def _extract_using_patterns(cls, text, patterns):
        """
        Extract text using a list of predefined patterns.

        Args:
            text (str): The input text.
            patterns (list): A list of regular expressions.

        Returns:
            list: A list of extracted text matching the patterns.
        """
        results = []
        for pattern in patterns:
            results.extend(re.findall(pattern, text))
        return results

# Example usage:
#if __name__ == "__main__":
#    text = "Sample text with a phone number (123) 456-7890 and an email address example@email.com."
#    print("Phone numbers:", InfoExtractor.extract_phone_numbers(text))
#    print("Links:", InfoExtractor.extract_links(text))
#    print("Emails:", InfoExtractor.extract_emails(text))
