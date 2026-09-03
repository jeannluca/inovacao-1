import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [images, setImages] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchImages();
  }, []);

  const fetchImages = async () => {
    try {
      const response = await fetch('http://localhost:8000/images');
      const data = await response.json();
      setImages(data);
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      setSelectedFile(null);
      setPreview(null);
      fetchImages();
    } catch (error) {
      console.error('Error uploading image:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await fetch(`http://localhost:8000/images/${id}`, {
        method: 'DELETE',
      });
      fetchImages();
    } catch (error) {
      console.error('Error deleting image:', error);
    }
  };

  const handlePreview = (id) => {
    const imageUrl = `http://localhost:8000/images/${id}`;
    setPreview(imageUrl);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Gerenciador de Imagens</h1>
      </header>

      <main className="App-main">
        <section className="upload-section">
          <h2>Enviar Imagem</h2>
          <div className="upload-area">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              id="file-input"
            />
            <label htmlFor="file-input" className="file-label">
              Selecionar Arquivo
            </label>
            {selectedFile && <p className="file-name">{selectedFile.name}</p>}
            {preview && (
              <div className="preview-container">
                <img src={preview} alt="Preview" className="preview-image" />
              </div>
            )}
            <button
              onClick={handleUpload}
              disabled={!selectedFile || uploading}
              className="upload-button"
            >
              {uploading ? 'Enviando...' : 'Enviar Imagem'}
            </button>
          </div>
        </section>

        <section className="table-section">
          <h2>Imagens Salvas</h2>
          <table className="images-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nome do Arquivo</th>
                <th>Tipo</th>
                <th>Data de Criação</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {images.map((image) => (
                <tr key={image.id}>
                  <td>{image.id}</td>
                  <td>{image.filename}</td>
                  <td>{image.content_type}</td>
                  <td>{new Date(image.created_at).toLocaleString()}</td>
                  <td>
                    <button
                      onClick={() => handlePreview(image.id)}
                      className="action-button preview-button"
                    >
                      Pré-visualizar
                    </button>
                    <button
                      onClick={() => handleDelete(image.id)}
                      className="action-button delete-button"
                    >
                      Excluir
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {images.length === 0 && (
            <p className="no-images">Nenhuma imagem salva ainda.</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
