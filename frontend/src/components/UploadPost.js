import React, { useState } from 'react';
import scoreService from '../services/scoreService';

const UploadPost = () => {
    const [selectedImage, setSelectedImage] = useState(null); // 選擇的圖片檔案
    const [previewImage, setPreviewImage] = useState(null);   // 圖片預覽
    const [uploadStatus, setUploadStatus] = useState('');     // 上傳狀態訊息

    // 處理圖片選擇事件
    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedImage(file);
            setPreviewImage(URL.createObjectURL(file));
            setUploadStatus('');
        }
    };

    // 處理圖片上傳
    const handleUpload = async () => {
        if (!selectedImage) {
            setUploadStatus('Please select an image to upload.');
            return;
        }

        setUploadStatus('Uploading...');
        const formData = new FormData();
        formData.append('photo', selectedImage);

        try {
            const response = await scoreService.uploadPost(formData);
            setUploadStatus(`Upload Successful! Post ID: ${response.data.postId}`);
            setSelectedImage(null);
            setPreviewImage(null);
        } catch (error) {
            console.error('Failed to upload image:', error);
            setUploadStatus('Upload Failed. Please try again.');
        }
    };

    return (
        <div className="upload-post-container">
            <h2>Upload Your Check-in Photo</h2>

            {/* 圖片預覽 */}
            {previewImage && (
                <div className="image-preview">
                    <img src={previewImage} alt="Preview" width="100%" />
                </div>
            )}

            {/* 圖片上傳輸入 */}
            <div className="file-input">
                <label htmlFor="fileUpload">Select a photo to upload:</label>
                <input
                    type="file"
                    id="fileUpload"
                    accept="image/*"
                    onChange={handleImageChange}
                />
            </div>

            {/* 上傳按鈕 */}
            <button onClick={handleUpload}>Upload Photo</button>

            {/* 上傳狀態 */}
            {uploadStatus && <p className="status-message">{uploadStatus}</p>}
        </div>
    );
};

export default UploadPost;
