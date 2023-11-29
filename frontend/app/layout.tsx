import { ReduxProvider } from './redux/provider'
import './globals.css'

export const metadata = {
  title: 'Antibiotic Picker',
  description: 'Created by Darshan Kalola'
}

export default function RootLayout ({ children }: { children: React.ReactNode }): any {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Karla&family=Merriweather:wght@300&display=swap" rel="stylesheet" />
      </head>
      <body className="flex flex-row justify-center my-10">
        <div className="">
          <ReduxProvider>
            {children}
          </ReduxProvider>
        </div>
      </body>
    </html>
  )
}
