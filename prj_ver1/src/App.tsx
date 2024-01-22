import Info from './pages/Info'
import MyImages from './pages/MyImages'
import Result from './pages/Result'
import {Div} from './components'

export default function App() {
  return (
    <main
      className="flex"
      style={{
        height: '100vh',
        alignItems: 'center',
        backgroundColor: '#F0E4E1',
        overflowY: 'auto'
      }}>
      <Div
        width="30%"
        minWidth="30%"
        height="95vh"
        minHeight="95vh"
        style={{borderRight: '1px solid gray'}}>
        <Info />
      </Div>
      <Div
        width="37%"
        minWidth="37%"
        height="95vh"
        minHeight="95vh"
        style={{borderRight: '1px solid gray'}}>
        <MyImages />
      </Div>
      <Div width="33%" minWidth="33%" height="95vh" minHeight="95vh">
        <Result />
      </Div>
    </main>
  )
}
