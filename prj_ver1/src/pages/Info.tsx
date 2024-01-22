import {useMemo, useCallback, useState} from 'react'
import type {ChangeEvent} from 'react'
import {Title, Subtitle} from '../components'

export default function Info() {
  /* 퍼스널컬러 배열 */
  const pColors = useMemo(
    () => [
      '봄 웜 라이트',
      '봄 웜 브라이트',
      '봄 웜 비비드',
      '여름 쿨 라이트',
      '여름 쿨 뮤트',
      '여름 쿨 소프트',
      '가을 웜 뮤트',
      '가을 웜 소프트',
      '가을 웜 딥',
      '겨울 쿨 딥',
      '겨울 쿨 클리어',
      '겨울 쿨 브라이트',
      '모름'
    ],
    []
  )

  /* 사용자가 선택한 버튼을 확인하기 위한 변수들 */
  const [selectedColor, setSelectedColor] = useState<string>(pColors[0])
  const onChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    setSelectedColor(notUsed => e.target.value)
  }, [])

  /* 라디오 버튼 생성 */
  const radioInputs = useMemo(
    () =>
      pColors.map((value, index) => (
        <label key={index} className="flex justify-start cursor-pointer label">
          <input
            type="radio"
            name="colors"
            className="mr-2 radio radio-primary"
            style={{width: '1rem', height: '1rem'}}
            checked={value === selectedColor}
            defaultValue={value}
            onChange={onChange}
          />
          <span className="label-text text-xs">{value}</span>
        </label>
      )),
    [pColors, selectedColor, onChange]
  )

  /* 라디오 버튼 3열로 맞추기 */
  const radioInputsRows = useMemo(() => {
    const rows = []
    for (let i = 0; i < radioInputs.length; i += 3) {
      rows.push(radioInputs.slice(i, i + 3))
    }
    return rows
  }, [radioInputs])

  /* 결과 반환 */
  return (
    <section className="mt-4">
      <Title>퍼스널컬러 정보</Title>
      <div className="flex flex-col  justify-center mt-4">
        <Subtitle>Selected: {selectedColor}</Subtitle>
        <div className="flex flex-wrap p-4 mt-4">
          {radioInputsRows.map((row, rowIndex) => (
            <div key={rowIndex} className="flex flex-grow">
              {row}
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}