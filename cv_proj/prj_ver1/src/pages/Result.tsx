import {useState, useEffect} from 'react'
import {Title, Subtitle} from '../components'
import * as D from '../data'
import axios from 'axios'

export default function Result() {
  const [resultData, setResultData] = useState({
    count: 0,
    upper: [],
    lower: []
  })

  /* 백엔드에서 데이터 가져오기 */
  useEffect(() => {
    axios
      .get('백엔드_url...')
      .then(response => {
        setResultData(response.data)
      })
      .catch(error => {
        console.error('Error fetching data:', error)
      })
  }, [])

  return (
    <main className="mt-4 ml-4">
      <Title>추천 코디</Title>
      <div className="flex flex-row">
        {/* 상의 3벌 데이터 가져오기 */}
        {resultData.upper.map((upper, index) => (
          <section key={index} className="mt-6 mr-4">
            <div>
              <Subtitle>상의 {index + 1}</Subtitle>
              <p className="mt-4 ml-4">
                {/* 이미지 url 가져오기 */}
                <img
                  src={upper.image_url}
                  width={100}
                  height={100}
                  alt={`Upper ${index + 1}`}
                />
                {/* 구매링크 가져오기 */}
                <div className="mt-3 text-sm font-bold">
                  <a href={upper.shopping_url} target="_blank" rel="noopener noreferrer">
                    구매 링크
                  </a>
                </div>
              </p>
            </div>
          </section>
        ))}

        {/* 하의 3벌 데이터 가져오기 */}
        {resultData.lower.map((lower, index) => (
          <section key={index} className="mt-6 mr-4">
            <div>
              <Subtitle>하의 {index + 1}</Subtitle>
              <p className="mt-4 ml-4">
                {/* 이미지 url 가져오기 */}
                <img
                  src={lower.image_url}
                  width={100}
                  height={100}
                  alt={`Lower ${index + 1}`}
                />
                {/* 구매링크 가져오기 */}
                <div className="mt-3 text-sm font-bold">
                  <a href={lower.shopping_url} target="_blank" rel="noopener noreferrer">
                    구매 링크
                  </a>
                </div>
              </p>
            </div>
          </section>
        ))}
      </div>
    </main>
  )
}
