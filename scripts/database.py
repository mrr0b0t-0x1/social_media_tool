"""
Social Media Tool - A tool to gather information about a user from multiple social networks
Copyright (C) 2021  Arpan Adlakhiya, Aditya Mahakalkar, Nihal Nakade and Renuka Lakhe

This file is part of Social Media Tool.

Social Media Tool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Social Media Tool is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Social Media Tool.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from pathlib import Path

from globals import ROOT_DIR

class DatabaseConnection(object):

    db, user, username, result_dir, site_dirs = None, None, None, None, None

    profile_urls = {
        'twitter': 'https://mobile.twitter.com/',
        'facebook': 'https://www.facebook.com/',
        'instagram': 'https://www.instagram.com/',
        'reddit': 'https://www.reddit.com/user/'
    }

    def __init__(self, username):
        # Make a database connection and return it
        self.db = TinyDB(ROOT_DIR / "scripts" / "database" / "db.json", indent=2, storage=CachingMiddleware(JSONStorage))
        self.user = Query()
        self.username = username
        self.result_dir = ROOT_DIR / "scripts" / "results" / username

    def __enter__(self):
        # Return the database connection
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Make sure the database connection gets closed
        self.db.close()

    # Check if user exists in DB
    def check_user(self):
        if self.result_dir.exists():
            return self.db.contains(self.user.name == self.username)
        else:
            return False

    # Get user data from DB
    def get_data(self):
        if self.result_dir.exists():
            if self.check_user():
                return self.db.get(self.user.name == self.username)

    # Update user data, insert if does not exist
    def update_user(self):

        def set_nested(path, val):
            def transform(doc):
                current = doc
                for key in path[:-1]:
                    current = current[key]
                current[path[-1]] = val

            return transform

        def update_data():
            if self.check_user():
                doc_id = self.db.get(self.user.name == self.username).doc_id

                self.site_dirs = self.result_dir.glob('*/')

                for site in self.site_dirs:
                    site_name = str(site.parts[-1])

                    # Update data file paths
                    data_files = site.glob('*.json')
                    for file in data_files:
                        filename = str(file.parts[-1].split('.json')[0])

                        self.db.update(set_nested([
                            'sites_found',
                            site_name,
                            'profile_url'
                        ], self.profile_urls[site_name] + self.username), doc_ids=[doc_id])

                        self.db.update(set_nested([
                            'sites_found',
                            site_name,
                            filename
                        ], str(file)), doc_ids=[doc_id])

                    # Update image file paths for instagram
                    if site_name == 'instagram':
                        image_files = list(filter(lambda p: p.suffix in ['.jpg', '.png'], site.glob('*.*')))
                        image_files.sort(key=os.path.getmtime, reverse=True)

                        self.db.update(set_nested([
                            'sites_found',
                            site_name,
                            'photos',
                        ], {}), doc_ids=[doc_id])

                        for i, file in enumerate(image_files):
                            self.db.update(set_nested([
                                'sites_found',
                                site_name,
                                'photos',
                                i
                            ], str(file)), doc_ids=[doc_id])

        def insert_user():
            self.site_dirs = self.result_dir.glob('*/')

            self.db.insert({
                'name': self.username,
                'sites_found': {
                    str(site.parts[-1]): {
                        'dir_url': str(site),
                    } for site in self.site_dirs
                }
            })

        if self.result_dir.exists():
            if not self.check_user():
                insert_user()

            update_data()

    # Remove user
    def remove_user(self, flag='r'):

        if self.result_dir.exists():
            if self.check_user():
                self.site_dirs = self.result_dir.glob('*/')

                doc_id = self.db.get(self.user.name == self.username).doc_id

                if flag == 'r':
                    self.db.remove(doc_ids=[doc_id])

                elif flag == 'rd':
                    self.db.remove(doc_ids=[doc_id])

                    for site in self.site_dirs:
                        files = [file for file in Path(site).iterdir()]

                        for file in files:
                            if file.is_file():
                                file.unlink()

                        if not any(site.iterdir()):
                            site.rmdir()

                    if not any(self.result_dir.iterdir()):
                        self.result_dir.rmdir()

    # Re-index DB in case of any operation failure
    def reindex_db(self):
        data_dir = ROOT_DIR / "scripts" / "results"

        for user_dir in data_dir.iterdir():
            if user_dir.is_dir():
                uname = str(user_dir.parts[-1])

                self.username = uname
                self.result_dir = ROOT_DIR / "scripts" / "results" / uname

                if not self.check_user():
                    self.update_user()
                else:
                    self.remove_user()
                    self.update_user()
