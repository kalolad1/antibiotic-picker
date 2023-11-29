'use client'

import { useEffect, useState } from 'react'
import { useAppSelector, type AppDispatch } from '../redux/store'
import { fetchRegimenSearchResults } from '../api'
import { useDispatch } from 'react-redux'
import { setRegimen, type Regimen, type Prescription } from '../redux/features/regimen/regimen_slice'
import { setQueryData } from '../redux/features/query_data/query_data_slice'

function RegimenSearchResultsPage (): any {
  const [loading, setLoading] = useState(true)
  const handp = useAppSelector((state) => state.handp.text)
  const regimen = useAppSelector((state) => state.regimen.value)
  const queryData = useAppSelector((state) => state.queryData.value)

  const dispatch = useDispatch<AppDispatch>()

  useEffect(() => {
    fetchRegimenSearchResults(handp)
      .then((data) => {
        dispatch(setRegimen(data.regimen))
        dispatch(setQueryData(data.query_data))
      })
      .finally(() => {
        setLoading(false)
      })
      .catch((err) => {
        console.log(err)
      })
  }, [])

  if (loading) {
    return (
      <div>
        LOADING...
      </div>
    )
  }

  return (
    <div className="flex flex-col space-y-10 py-10">
      <RegimenPreview regimen={regimen} diagnosis={queryData.diagnosis} />
      <br />
      <h1 className="text-center font-merriweather">For your <b>{queryData.sex}</b>, <b>{queryData.age}-year-old</b> patient with <b>{queryData.diagnosis}</b>.</h1>
    </div>
  )
}

function RegimenPreview (props: { regimen: Regimen, diagnosis: string }): any {
  const prescriptionPreviews = props.regimen.prescriptions.map(
    (prescription, index) => <PrescriptionPreview key={index} prescription={prescription}/>
  )
  return (
    <div className="flex flex-col items-center space-y-4">
      {prescriptionPreviews}
    </div>
  )
}

function PrescriptionPreview (props: { prescription: Prescription }): any {
  return (
    <div className="flex flex-col w-4/5 border border-2 border-black rounded-lg text-gray-900 p-4">
      <div>
        <h3 className="font-karla text-2xl mb-2">{props.prescription.drug}</h3>
      </div>
      <div className="flex flex-row justify-between font-merriweather text-md">
        <h5>{props.prescription.dose}</h5>
        <h5>•</h5>
        <h5>{props.prescription.frequency}</h5>
        <h5>•</h5>
        <h5>{props.prescription.end_day - props.prescription.start_day + 1} days</h5>
        <h5>•</h5>
        <h5>{props.prescription.route}</h5>
      </div>
    </div>
  )
}

export default RegimenSearchResultsPage
