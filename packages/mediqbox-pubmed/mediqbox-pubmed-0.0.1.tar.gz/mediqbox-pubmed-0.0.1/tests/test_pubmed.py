from dotenv import load_dotenv

from mediqbox.pubmed.pubmed import (
  Pubmed,
  PubmedConfig,
  PubmedInputData,
)

load_dotenv()

from tests.settings import settings

pubmed = Pubmed(config=PubmedConfig(
  ncbi_email=settings.NCBI_EMAIL,
  ncbi_api_key=settings.NCBI_API_KEY
))

def test_pubmed():
  result = pubmed.process(PubmedInputData(
    term="10.1080/1120009X.2021.1937782[doi]"
  ))

  assert result.count == 1 and result.retmax == 1 and len(result.records) == 1

  print(result)


if __name__ == '__main__':
  test_pubmed()