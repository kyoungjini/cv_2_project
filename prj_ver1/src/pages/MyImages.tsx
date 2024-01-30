import type {ChangeEvent, DragEvent} from 'react'
import {useState, useRef, useCallback, useMemo} from 'react'
import {useToggle} from '../hooks'
import {Title, Div, Subtitle} from '../components'
import {imageFileReaderP} from '../utils'

export default function MyImages() {
  const [imageUrls, setImageUrls] = useState<string[]>([])
  const [error, setError] = useState<Error | null>(null)
  const [loading, toggleLoading] = useToggle(false)

  const inputRef = useRef<HTMLInputElement>(null)
  const onDivClick = useCallback(() => inputRef.current?.click(), [])

  const makeImageUrls = useCallback(
    (files: File[]) => {
      /* 이미지 파일 개수 제한 */
      if (imageUrls.length + files.length > 9) {
        setError(new Error('이미지는 최대 9개까지만 추가할 수 있습니다!'))
        return
      }

      const promises = Array.from(files).map(imageFileReaderP)
      toggleLoading()
      Promise.all(promises)
        .then(urls => setImageUrls(imageUrls => [...urls, ...imageUrls]))
        .catch(setError)
        .finally(toggleLoading)
    },
    [imageUrls, toggleLoading]
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

  /* 이미지 업로드 취소 기능 추가하기 */
  const onCacelClick = useCallback(
    (index: number) => {
      const uploadedImages = [...imageUrls]
      /* 해당 인덱스의 이미지 제거 */
      uploadedImages.splice(index, 1)
      setImageUrls(uploadedImages)
    },
    [imageUrls]
  )

  /* 이미지 파일 화면에 나타내기 (취소 버튼 있는 ver.) */
  const images = useMemo(
    () =>
      imageUrls.map((url, index) => (
        <div key={index} className="relative m-2">
          {/* 이미지 파일 태그 */}
          <Div
            src={url}
            className="bg-transparent bg-center bg-no-repeat bg-contain"
            width="7rem"
            height="7rem"
          />
          {/* 취소 버튼 태그 */}
          <button
            className="absolute top-0 right-0 text-white bg-red-500 rounded-full"
            style={{width: '1.0rem', height: '1.0rem', fontSize: '0.65rem'}}
            onClick={() => onCacelClick(index)}>
            X
          </button>
        </div>
      )),
    [imageUrls, onCacelClick]
  )

  /* 이미지 파일 화면에 나타내기 (취소 버튼 없는 ver.)
  // prettier-ignore
  const images = useMemo( () =>
    imageUrls.map((url, index) => (
      <Div key={index} src={url}
        className="m-2 bg-transparent bg-center bg-no-repeat bg-contain"
        width="7rem" height="7rem" />
    )), [imageUrls])
  */

  // prettier-ignore
  return (
    <section className="mt-4">
      <div className='ml-4'>
        <Title>당신의 사진</Title>
        <Subtitle>(최대 9개까지 넣을 수 있어용)</Subtitle>
        {error && (
          <div className="flex items-center justify-center p-4 mt-4 bg-red-200">
            <p className="text-base text-red-500 text-bold">{error.message}</p>
          </div>
        )}

        <div onClick={onDivClick}
          className="w-full mt-4 ml-4 bg-gray-300 border border-gray-500" style={{width: '10rem', height: '2rem'}}>
          {loading && (
            <div className="flex items-center justify-center">
              <button className="btn btn-circle loading"></button>
            </div>
          )}

          <div onDragOver={onDivDragOver} onDrop={onDivDrop}
            className="flex flex-col items-center h-40 mt-1 cursor-pointer">
            <p className="text-sm">이미지 파일 가져오기</p>
          </div>
          <input ref={inputRef} onChange={onInputChange}
            multiple className="hidden" type="file" accept="image/*" />
        </div>
      </div>

      <div className="flex flex-wrap justify-center mt-2">{images}</div>
    </section>
  )
}
