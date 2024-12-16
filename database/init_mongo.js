// init_mongo.js

// 初始化 users 集合
db = db.getSiblingDB("team_event"); // 資料庫名稱：team_event

db.users.insertMany([
  { 
    "username": "user1",
    "email": "user1@example.com",
    "teams": [],
    "created_at": new Date()
  },
  { 
    "username": "user2",
    "email": "user2@example.com",
    "teams": [],
    "created_at": new Date()
  }
]);

// 初始化 teams 集合
db.teams.insertMany([
  { 
    "team_name": "Team Alpha",
    "members": ["user1"],
    "new_members_count": 1,
    "created_at": new Date()
  },
  { 
    "team_name": "Team Beta",
    "members": ["user2"],
    "new_members_count": 0,
    "created_at": new Date()
  }
]);

// 初始化 scores 集合
db.scores.insertMany([
  {
    "team_name": "Team Alpha",
    "score": 10,
    "time_difference": 5,
    "new_members_count": 1,
    "updated_at": new Date()
  },
  {
    "team_name": "Team Beta",
    "score": 8,
    "time_difference": 7,
    "new_members_count": 0,
    "updated_at": new Date()
  }
]);

print("MongoDB initialization completed.");
