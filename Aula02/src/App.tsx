import { useState, useEffect } from 'react'
import { Fragment } from 'react/jsx-runtime'
function App() {
  const [clique,setClique] = useState<number>(0);

  useEffect(() => {
    console.log('carregou')
  }, [])

  return (
    <Fragment>
<button onClick={() => setClique(clique + 1)}>Clique aqui</button>
<p>Você clicou {clique} vezes</p>
    </Fragment>
  )
}

export default App