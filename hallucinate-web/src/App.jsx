import { useEffect, useState } from 'react';
import { useDebounce } from "use-debounce";

import './App.css';

async function getPromptsVariants(prompt) {
  const url = `http://0.0.0.0:8000/generate/${prompt}`

  const response = await fetch(url)
  const data = await response.json()
  return data["prompts"]
}

function App() {
  const [images, setImages] = useState([])
  const [prompt, setPrompt] = useState("")
  const [debouncedPrompt] = useDebounce(prompt, 500);

  const [serviceMessage, setServiceMessage] = useState("")

  useEffect(() => {
    if (debouncedPrompt) {
      setServiceMessage("Loading prompts...")
      getPromptsVariants(debouncedPrompt).then((prompts) => {
        setServiceMessage("Prompts loaded.")
        resetImages(prompts)
      })
    }
  }, [debouncedPrompt])

  function resetImages(prompts) {
    setImages(prompts)
  }

  function loadMore() {
    setServiceMessage("Loading more prompts...")
    getPromptsVariants(prompt).then((prompts) => {
      setServiceMessage("More prompts loaded.")
      setImages([...images, ...prompts])
    })
  }

  function onScrollToBottom() {
    loadMore()
  }

  return (
    <>
      <h1>Hallucinate</h1>
      Propmt: <PromptField onPrompt={setPrompt} />
      <ImageFeed images={images} onScrollToBottom={onScrollToBottom} />
      <button onClick={() => loadMore()}>Load More</button>
      <div>Service: {serviceMessage}</div>
    </>
  )
}

function imageUrl(prompt) {
  return `http://0.0.0.0:8001/generate/${prompt}`
}

function ImageFeed({ images, onScrollToBottom }) {
  const handleScroll = (event) => {
    const { scrollTop, clientHeight, scrollHeight } = event.target;
    if (scrollHeight - scrollTop === clientHeight) {
      onScrollToBottom();
    }
  };

  return (
    <div className="image-feed" onScroll={handleScroll}>
      {images.map((image, index) => (
        <img key={index} src={imageUrl(image)} />
      ))}
    </div>
  );
}

function PromptField({ onPrompt }) {
  const handleSearch = (event) => {
    const searchTerm = event.target.value
    onPrompt(searchTerm)
  }

  return (
    <input type="text" placeholder="Enter Prompt" onChange={handleSearch} />
  )
}

export default App

