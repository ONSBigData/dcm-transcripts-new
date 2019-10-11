import SegmentList from './SegmentList'
import FileLoader from './FileLoader'
import { useState } from "react";

const loadedTrData = require('../final.json');

export default function App() {
    const [trData, setTrData] = useState(loadedTrData);
    
    return (
        <>
            <FileLoader setData={setTrData} />

            <SegmentList
                segments={trData}
            />
        </>
    );
  }
  