import type {ChangeEvent, DragEvent} from 'react'
import {useState, useRef, useCallback, useMemo} from 'react'
import {useToggle} from '../hooks'
import {Title, Subtitle} from '../components'
import {imageFileReaderP} from '../utils'
import * as D from '../data'

export default function Result() {
  return (
    <section className="mt-4">
      <Title>추천 코디</Title>
      <div className="mt-4">
        <Subtitle>상의</Subtitle>
        <div className="mt-4 ml-4">
          <img src={D.randomAvatar()} width={100} height={100} />
        </div>
      </div>
      <div className="mt-4">
        <Subtitle>하의</Subtitle>
        <div className="mt-4 ml-4">
          <img src={D.randomAvatar()} width={100} height={100} />
        </div>
      </div>
    </section>
  )
}
