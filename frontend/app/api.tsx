import * as constants from './constants'

export async function fetchRegimenSearchResults (handpText: string): Promise<any> {
  const data = {
    handp_text: handpText
  }
  const fetchData = {
    method: 'POST',
    body: JSON.stringify(data),
    headers: new Headers({
      'Content-Type': 'application/json; charset=UTF-8',
    })
  }
  const response = await fetch(constants.REGIMEN_SEARCH_ENDPOINT, fetchData)

  return await response.json()
}

export async function fetchReferenceDocument (diagnosis: string): Promise<any> {
  const fetchData = {
    method: 'GET',
    headers: new Headers({
      'Content-Type': 'application/json; charset=UTF-8'
    })
  }
  return await fetch(constants.REFERENCE_DOC_ENDPOINT + `/${diagnosis}`, fetchData)
}
