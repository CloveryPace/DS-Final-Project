import React from 'react';
import Auth from './components/Auth';
import TeamRegistration from './components/TeamRegistration';
import UploadPost from './components/UploadPost';
import RankingBoard from './components/RankingBoard';

function App() {
    return (
        <div className="App">
            <h1>Team Check-in Competition</h1>
            {/* 登入與註冊 */}
            <Auth />

            <hr />

            {/* 團隊註冊與加入 */}
            <TeamRegistration />

            <hr />

            {/* 上傳打卡照片 */}
            <UploadPost />

            <hr />

            {/* 即時排名看板 */}
            <RankingBoard />
        </div>
    );
}

export default App;
