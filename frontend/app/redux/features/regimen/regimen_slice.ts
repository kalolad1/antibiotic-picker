import { type PayloadAction, createSlice } from '@reduxjs/toolkit'

export interface Prescription {
  drug: string
  dose: string
  frequency: string
  route: string
  start_day: number
  end_day: number
}

export interface Regimen {
  prescriptions: Prescription[]
}

interface InitialState {
  value: Regimen
}

export const regimenSlice = createSlice({
  name: 'regimen',
  initialState: {
    value: {
      prescriptions: []
    }
  } as InitialState,
  reducers: {
    setRegimen: (_, action: PayloadAction<Regimen>) => {
      return {
        value: action.payload
      }
    }
  }
})

export const { setRegimen } = regimenSlice.actions
export default regimenSlice.reducer
