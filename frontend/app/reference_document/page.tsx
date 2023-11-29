'use client'

import ReactMarkdown from 'react-markdown'

import { useSearchParams } from 'next/navigation'
import { useState, useEffect } from 'react'
import { fetchReferenceDocument } from '../api'

function ReferenceDocumentPage (): any {
  const searchParams = useSearchParams()
  const diagnosis = searchParams.get('diagnosis')

  const [text, setText] = useState(null)

  useEffect(() => {
    fetchReferenceDocument(diagnosis!)
      .then(async (response) => {
        return await response.json()
      })
      .then((data) => {
        setText(data.text)
        console.log(data.text)
      })
      .catch((err) => {
        console.log(err)
      })
  }, [])

  return (
        <div>
          <ReactMarkdown className="markdown font-merriweather" children={text!}/>
        </div>
  )
}

export default ReferenceDocumentPage
