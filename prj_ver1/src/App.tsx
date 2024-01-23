import Info from './pages/Info'
import MyImages from './pages/MyImages'
import Result from './pages/Result'
import {Div, Title} from './components'

export default function App() {
  return (
    <main
      style={{
        backgroundColor: '#F8E4E1'
      }}>
      <Div
        height="7vh"
        style={{borderBottom: '1px solid gray', paddingLeft: '20px', paddingTop: '5px'}}>
        <p className="text-lg font-bold">[코디 추천해드립니당]</p>
      </Div>
      <div
        className="flex"
        style={{
          height: '93vh',
          alignItems: 'center',
          overflowY: 'auto'
        }}>
        <Div
          width="30%"
          minWidth="30%"
          height="90vh"
          minHeight="90vh"
          style={{borderRight: '1px solid gray'}}>
          <Info />
        </Div>
        <Div
          width="37%"
          minWidth="37%"
          height="90vh"
          minHeight="90vh"
          style={{borderRight: '1px solid gray'}}>
          <MyImages />
        </Div>
        <Div width="33%" minWidth="33%" height="90vh" minHeight="90vh">
          <Result />
        </Div>
      </div>
    </main>
  )
}
