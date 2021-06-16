/**
 * Social Media Tool - A tool to gather information about a user from multiple social networks
 * Copyright (C) 2021  Arpan Adlakhiya, Aditya Mahakalkar, Nihal Nakade and Renuka Lakhe
 *
 * This file is part of Social Media Tool.
 *
 * Social Media Tool is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Social Media Tool is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Social Media Tool.  If not, see <https://www.gnu.org/licenses/>.
 */

const about_twitter = {
    "id": '',
    "name": '',
    "username": '',
    "bio": '',
    "location": '',
    "url": '',
    "join date": '',
    "join time": '',
    "tweets": '',
    "following": '',
    "followers": '',
    "likes": '',
    "media": '',
    "private": '',
    "verified": '',
    "profile image url": '',
    "background image": ''
}

const timeline_twitter = {
    "link": '',
    "created at": '',
    "username": '',
    "name": '',
    "mentions": [],
    "urls": [],
    "photos": [],
    "retweets count": '',
    "likes count": '',
    "hashtags": []
}

const posts_fb = {
    "post url": '',
    "username": '',
    "text": '',
    "date": '',
    "time": '',
    "images": [],
    "video": '',
    "likes": '',
    "comments": '',
    "shares": '',
    "link": ''
}

const about_insta = {
    "username": '',
    "name": '',
    "followers": '',
    "following": '',
    "posts img": '',
    "posts vid": '',
    "reels": '',
    "bio": '',
    "external url": '',
    "private": '',
    "verified": '',
    "profile img": '',
    "business account": '',
    "most used tags": {},
    "most used mentions": {}
}

const posts_insta = {
    "images": [],
    "comments": '',
    "timestamp": '',
    "likes": '',
    "caption": ''
}

const about_reddit = {
    "url": '',
    "title": '',
    "name": '',
    "total karma": '',
    "created": ''
}

const posts_reddit = {
    "permalink": '',
    "subreddit": '',
    "text": '',
    "title": '',
    "image": '',
    "upvotes": '',
    "downvotes": '',
    "created": '',
    "author": '',
    "number of comments": '',
    "url": ''
}

const map_obj = {
    "about_twitter": about_twitter,
    "timeline_twitter": timeline_twitter,
    "posts_fb": posts_fb,
    "about_insta": about_insta,
    "posts_insta": posts_insta,
    "about_reddit": about_reddit,
    "posts_reddit": posts_reddit,
}

function getSectionName(username, section) {
    let sectionName = section.split(username + '-')[1];
    if (sectionName.includes("fb")) {
        sectionName = sectionName.substring(0, sectionName.lastIndexOf("-"));
    }

    return sectionName.replace('-','_');
}

function createNewInstance(key) {
    const obj = {}
    Object.keys(map_obj[key]).forEach(function (k) {
        obj[k] = map_obj[key][k]
    });
    return obj
}

function filter(username, data, site, section) {
    const sectionName = getSectionName(username, section)

    let check = map_obj[sectionName]

    if (check) {
        if (sectionName.includes("about")) {
            // let obj = map_obj[sectionName]
            let obj = createNewInstance(sectionName)

            if (sectionName === "about_reddit") {
                Object.keys(data["data"]).forEach(function (key) {
                    let key_in_obj = key.split('_').join(' ')

                    if (key === "subreddit") {
                        obj["title"] = data["data"]["subreddit"]["title"]
                        obj["url"] = data["data"]["subreddit"]["url"]
                    }
                    else if (key_in_obj in obj && data["data"][key] !== '' && data["data"][key] !== null) {
                        obj[key_in_obj] = data["data"][key]
                    }
                });
            } else {
                Object.keys(data).forEach(function (key) {
                    let key_in_obj = key.split('_').join(' ')

                    if (key_in_obj in obj && data[key] !== '' && data[key] !== null) {
                        obj[key_in_obj] = data[key]
                    }
                });
            }

            return obj

        } else {
            let posts = {}

            if (sectionName === "posts_reddit") {
                data = data["data"]["children"]
                if (Array.isArray(data)) {
                    data.forEach(function (post, index) {
                        if (Object.keys(posts).length < 10) {
                            // let obj = map_obj[sectionName]
                            let obj = createNewInstance(sectionName)
                            Object.keys(post["data"]).forEach(function (key) {
                                let key_in_obj = key.split('_').join(' ')

                                if (key === "selftext")
                                    obj["text"] = post["data"]["selftext"]
                                else if (key === "ups")
                                    obj["upvotes"] = post["data"]["ups"]
                                else if (key === "downs")
                                    obj["downvotes"] = post["data"]["downs"]
                                else if (key === "num_comments")
                                    obj["number of comments"] = post["data"]["num_comments"]
                                else if (key === "preview")
                                    obj["image"] = post["data"][key]["images"]["0"]["source"]["url"]

                                if (key_in_obj in obj && post["data"][key] !== '' && post["data"][key] !== null) {
                                    obj[key_in_obj] = post["data"][key]
                                }
                            });

                            posts[index] = obj
                        }
                    });
                }
            } else {
                Object.keys(data).forEach(function (post) {
                    // let obj = map_obj[sectionName]
                    let obj = createNewInstance(sectionName)
                    Object.keys(data[post]).forEach(function (key) {
                        let key_in_obj = key.split('_').join(' ')

                        if (key_in_obj in obj && data[post][key] !== '' && data[post][key] !== null) {

                            // for twitter timeline
                            if (key === "mentions" && Array.isArray(data[post][key]) && data[post][key].length > 0) {
                                data[post][key].forEach(function (item) {
                                    obj[key_in_obj].push(item["screen_name"])
                                });
                            }

                            // for fb date
                            else if (key === "time") {
                                const date_time = data[post]["time"].split(' ')
                                obj["date"] = date_time[0]
                                obj["time"] = date_time[1]
                            }
                            else {
                                obj[key_in_obj] = data[post][key]
                            }
                        }

                        // for insta
                        if (sectionName === "posts_insta") {
                            if (key === "info" && data[post][key] !== '' && data[post][key] !== null) {
                                Object.keys(data[post][key]).forEach( function (k) {
                                    if (k in obj) {
                                        obj[k] = data[post][key][k]
                                    }
                                });
                            }
                            if (key === "imgs" && Array.isArray(data[post][key]) && data[post][key].length > 0) {
                                let arr = []
                                data[post][key].forEach(img => {
                                    arr.push({
                                        "link": img["image url"],
                                        "accessibility": img["accessibility"]
                                    });
                                });
                                obj["images"] = arr
                            }
                        }
                    });

                    posts[post] = obj
                });
            }

            return posts
        }
    }
}


module.exports = {
    filterData: filter
}

