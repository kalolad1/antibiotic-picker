'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { setHandp } from './redux/features/handp/handp_slice'
import { useDispatch } from 'react-redux'
import { type AppDispatch } from './redux/store'

function HomePage (): any {
  return (
    <div className="flex justify-center items-center">
      <HAndPTextBoxForm />
    </div>
  )
}

function HAndPTextBoxForm (): any {
  const router = useRouter()
  const dispatch = useDispatch<AppDispatch>()

  function handleSubmit (event: any) {
    event.preventDefault()
    const formData = new FormData(event.target)
    const handpText = formData.get('inputText') as string
    dispatch(setHandp(handpText))
    router.push('regimen_searches/')
  }

  return (
    <form
      method="post"
      onSubmit={handleSubmit}
      className="flex flex-col justify-center items-center space-y-5"
    >
      <HandPTextBox />
      <GoButton />
    </form>
  )
}

function HandPTextBox (): any {
  const [inputTextValue, setInputTextValue] = useState('')

  const handleInputChange = (event: any) => {
    setInputTextValue(event.target.value)
  }

  return (
    <textarea
      name="inputText"
      value={inputTextValue}
      onChange={handleInputChange}
      rows={10}
      cols={60}
      placeholder="Paste H&P here"
      className="border border-2 border-black rounded-lg text-gray-900 p-2.5 font-merriweather"
    />
  )
}

function GoButton (): any {
  return (
    <button
      type="submit"
      className="button-17 font-karla"
    >
      Generate recommendations
    </button>
  )
}

export default HomePage
