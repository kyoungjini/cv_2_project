import type {ChangeEvent, DragEvent} from 'react'
import {useState, useRef, useCallback, useMemo} from 'react'
import {useToggle} from '../hooks'
import {Title, Div} from '../components'
import {imageFileReaderP} from '../utils'

export default function MyImages() {
  const [imageUrls, setImageUrls] = useState<string[]>([])
  const [error, setError] = useState<Error | null>(null)
  const [loading, toggleLoading] = useToggle(false)

  const inputRef = useRef<HTMLInputElement>(null)
  const onDivClick = useCallback(() => inputRef.current?.click(), [])

  const makeImageUrls = useCallback(
    (files: File[]) => {
      const promises = Array.from(files).map(imageFileReaderP)
      toggleLoading()
      Promise.all(promises)
        .then(urls => setImageUrls(imageUrls => [...urls, ...imageUrls]))
        .catch(setError)
        .finally(toggleLoading)
    },
    [toggleLoading]
  )

  const onInputChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      setError(null)
      const files = e.target.files
      files && makeImageUrls(Array.from(files))
    },
    [makeImageUrls]
  )

  const onDivDragOver = useCallback((e: DragEvent) => e.preventDefault(), [])
  const onDivDrop = useCallback(
    (e: DragEvent) => {
      e.preventDefault()
      setError(null)
      const files = e.dataTransfer?.files
      files && makeImageUrls(Array.from(files))
    },
    [makeImageUrls]
  )

  // prettier-ignore
  const images = useMemo( () =>
    imageUrls.map((url, index) => (
      <Div key={index} src={url}
        className="m-2 bg-transparent bg-center bg-no-repeat bg-contain"
        width="7rem" height="7rem" />
    )), [imageUrls])

  // prettier-ignore
  return (
    <section className="mt-4">
      <Title>당신의 사진</Title>
      {error && (
        <div className="p-4 mt-4 bg-red-200">
          <p className="text-3xl text-red-500 text-bold">{error.message}</p>
        </div>
      )}

      <div onClick={onDivClick}
        className="w-full ml-4 mt-4 bg-gray-300 border border-gray-500" style={{width: '10rem', height: '2rem'}}>
        {loading && (
          <div className="flex items-center justify-center">
            <button className="btn btn-circle loading"></button>
          </div>
        )}

        <div onDragOver={onDivDragOver} onDrop={onDivDrop}
          className="mt-1 flex flex-col items-center h-40 cursor-pointer">
          <p className="text-sm">이미지 파일 가져오기</p>
        </div>
        <input ref={inputRef} onChange={onInputChange}
          multiple className="hidden" type="file" accept="image/*" />
      </div>

      <div className="mt-2 flex flex-wrap justify-center">{images}</div>
    </section>
  )
}
