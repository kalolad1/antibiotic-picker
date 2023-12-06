import { type PayloadAction, createSlice } from '@reduxjs/toolkit'

export interface QueryData {
  age: number
  sex: string
  diagnosis: string
}

export const queryDataSlice: any = createSlice({
  name: 'queryData',
  initialState: {
    value: {
      age: 0,
      sex: '',
      diagnosis: ''
    }
  },
  reducers: {
    setQueryData: (_, action: PayloadAction<QueryData>) => {
      return {
        value: action.payload
      }
    }
  }
})

export const { setQueryData } = queryDataSlice.actions
export default queryDataSlice.reducer
