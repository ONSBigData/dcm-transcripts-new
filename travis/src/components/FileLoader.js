import { useRef } from "react";

export default function FileLoader({
    setData = (data) => null
}) {
    const fileInput = useRef(null);

    const onSubmit = (event) => {
        event.preventDefault();

        let file = fileInput.current.files[0];
        let reader = new FileReader();
        
        reader.onloadend = () => {
            setData(JSON.parse(reader.result))
        }
        reader.readAsText(file);
    };

    return (
        <form onSubmit={onSubmit}>
            <label>
                Load a file: <input type="file" ref={fileInput} />
            </label>
            <button type="submit">Submit</button>
        </form>
    );    
}