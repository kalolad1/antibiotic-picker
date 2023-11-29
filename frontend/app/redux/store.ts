import { configureStore } from '@reduxjs/toolkit'
import handpReducer from './features/handp/handp_slice'
import regimenReducer from './features/regimen/regimen_slice'
import queryDataReducer from './features/query_data/query_data_slice'
import { type TypedUseSelectorHook, useSelector } from 'react-redux'

export const store: any = configureStore({
  reducer: {
    handp: handpReducer,
    regimen: regimenReducer,
    queryData: queryDataReducer
  }
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
