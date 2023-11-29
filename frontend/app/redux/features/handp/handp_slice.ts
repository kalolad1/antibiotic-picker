import { type PayloadAction, createSlice } from '@reduxjs/toolkit'

export const handpSlice = createSlice({
  name: 'handp',
  initialState: {
    text: ''
  },
  reducers: {
    setHandp: (_, action: PayloadAction<string>) => {
      return {
        text: action.payload
      }
    }
  }
})

export const { setHandp } = handpSlice.actions
export default handpSlice.reducer
