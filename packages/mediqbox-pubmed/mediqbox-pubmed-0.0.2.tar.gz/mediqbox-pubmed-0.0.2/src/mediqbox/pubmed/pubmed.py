import logging

from Bio import Entrez, Medline
from pydantic import BaseModel, Field

from mediqbox.abc.abc_component import (
  AbstractComponent,
  ComponentConfig,
  InputData
)

class PubmedConfig(ComponentConfig):
  ncbi_email: str
  ncbi_api_key: str
  max_retries: int = Field(ge=1, le=3, default=3)

class PubmedInputData(InputData):
  term: str
  retmax: int = Field(ge=1, le=100, default=100)

class PubmedResult(BaseModel):
  count: int
  retmax: int
  records: list[dict]

class PubmedTooManyRetriesException(Exception):
  """Exception raised when too many retries occur"""
  def __init__(self, retries: int, message: str="Too many retries", *args):
    super().__init__(f"{message}: {retries} attempts made", *args)

class Pubmed(AbstractComponent):

  def process(self, input_data: PubmedInputData) -> PubmedResult:
    Entrez.email = self.config.ncbi_email
    Entrez.api_key = self.config.ncbi_api_key

    # Search
    retries = self.config.max_retries
    while retries:
      try:
        handle = Entrez.esearch('pubmed', input_data.term, retmax=input_data.retmax)
        search_record = Entrez.read(handle)
        break
      except Exception as e:
        logging.error(f"Pubmed searching error (will retry): {e}")
        retries -= 1
      finally:
        if handle:
          handle.close()

    # Fetch
    while retries:
      try:
        handle = Entrez.efetch('pubmed', id=search_record['IdList'], rettype='medline', retmode='text')
        fetch_records = Medline.parse(handle)
        result = PubmedResult(
          count=search_record['Count'],
          retmax=search_record['RetMax'],
          records=[],
          raw_records=[]
        )
        for record in fetch_records:
          result.records.append({
            'pmid': record.get('PMID', ''),
            'source': record.get('SO', ''),
            'title': record.get('TI', ''),
            'abstract': record.get('AB', ''),
            'journal': record.get('JT', ''),
            'issn': record.get('IS'),
            'keywords': record.get('OT', []),
            'languages': record.get('LA', []),
            'publication_types': record.get('PT', []),
            'publication_date': record.get('DP', ''),
            'authors': record.get('FAU') or record.get('AU', []),
            'pmc': record.get('PMC', '')
          })
        return result
      except Exception as e:
        logging.error(f"Pubmed fetching error (will retry): {e}")
        retries -= 1
      finally:
        if handle:
          handle.close()
    
    raise PubmedTooManyRetriesException(
      self.config.max_retries,
      "Too many errors when searching pubmed and fetching records"
    )