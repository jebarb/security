// Copyright (c) 2012, UNC Chapel Hill. All rights reserved.
// Author: Kevin Z. Snow
// Modifications: Andrew M. White
//
// Worlds simplest, most amazing, password cracking program
// AMW: Now with custom hash function!
//

// C++ Includes
#include <iostream>  // for cout
#include <iomanip>  // for setw, left
#include <fstream>  // for ifstream
#include <sstream>  // for stringstream
#include <string>  // for string
#include <vector>  // for vector

// C Includes
#include <stdlib.h>  // for exit
#include <string.h>  // for strnlen
#include <stdint.h>  // for typedefs
#include <sys/resource.h> // for setpriority

// Namespaces used
using std::cout;
using std::endl;
using std::ifstream;
using std::stringstream;
using std::string;
using std::pair;
using std::vector;

uint32_t MySubhashFunction(const uint8_t *key, size_t len) {
  uint32_t h = 1013; // my UID
  for (size_t i = 0; i < len; i++)
    h ^= (uint32_t)key[i] << 8*(i % 4);
  return h;
}

uint32_t OurSubhashFunction(const uint8_t *key, size_t len) {
  uint32_t h = 535590091; // class ID (535/590-091) 
  //
  // YOUR IMPLEMENTATION HERE
  //
}

uint64_t CustomHashFunction(const uint8_t *key, size_t len) {
  uint32_t mine = MySubhashFunction(key, len);
  uint32_t ours = OurSubhashFunction(key, len);
  return ((uint64_t)mine << 32) + (uint64_t)ours;
}

// We store each entry in the hash file as a user/hash string pair
typedef pair<string, string> UserHashPair;
// And we keep a vector of those pairs
typedef vector<UserHashPair> UserHashList;

// Reads in the users and password hashes from the given filename, parses,
// and stores them in our vector of UserHashPair's
void ReadPasswordHashList(const string& filename, UserHashList* userHashes) {
  ifstream hashFile(filename.c_str());
  if (!hashFile.is_open()) {
    cout << "Could not open user hash file: " << filename << endl;
    return;
  }
  string line;
  while (hashFile.good()) {
    getline(hashFile, line);
    size_t found = line.find_first_of(":");
    if (found == string::npos)
      continue;
    string user(line.substr(0, found));
    string hash(line.substr(found + 1, line.length() - found - 1));
    userHashes->push_back(UserHashPair(user, hash));
  }
  hashFile.close();
}

// Computes the hash of the guessed password, then compares
// it to each actual user password hash in the UserHashList.  If a match is
// found, the user and password are printed, and the user is removed from the
// UserHashList.
void TestGuessAgainstAllUsers(UserHashList* userHashes,
                              const string& guess) {
  // Compute the hash of the candidate password
  stringstream guessHash;
  uint64_t hash_value = CustomHashFunction((const uint8_t *)guess.c_str(), guess.length());
  guessHash << std::setw(16) << std::setfill('0') << std::hex << hash_value;

  // Compare it to the actual hash of each user's password
  for (UserHashList::iterator userHash_it = userHashes->begin();
       userHash_it < userHashes->end();) {
    UserHashPair& userHash = *userHash_it;
    const string& actualHash = userHash.second;
    if (actualHash.compare(guessHash.str()) == 0) {
      cout << std::setw(20) << std::left
           << guess << "(" << userHash.first << ")" << endl;
      userHash_it = userHashes->erase(userHash_it);
    } else {
      ++userHash_it;
    }
  }
}

// Generates candidate passwords and tests them against all users using:
//   TestGuessAgainstAllUsers(userHashes, "myguess");
void CrackPasswords(UserHashList* userHashes, string filename) {
  ifstream wordFile(filename.c_str());
  if (!wordFile.is_open()) {
    cout << "Could not open wordlist file" << endl;
    return;
  }
  string line;
  while (wordFile.good()) {
    getline(wordFile, line);
    TestGuessAgainstAllUsers(userHashes, line);
  }
  wordFile.close();
}

void CrackPasswordsWithStdin(UserHashList* userHashes) {
  string line;
  while(std::cin) {
    getline(std::cin, line);
    TestGuessAgainstAllUsers(userHashes, line);
  };
}

int main(int argc, char *argv[]) {
  setpriority(PRIO_PROCESS, 0, -20);
  if (argc != 3) {
    cout << "Usage: " << argv[0] << " <hash file> <word list>" << endl;
    cout << "    <hash file>: file containing 'username:hash'" << endl;
    cout << "    <word list>: candidate passwords (use '-' for stdin)" << endl;
    return 1;
  }

  string hash_filename(argv[1]);
  UserHashList userHashes;
  ReadPasswordHashList(hash_filename, &userHashes);

  cout << "Loaded " << userHashes.size() << " password hashes." << endl;
  if (userHashes.size() == 0) {
    return 1; 
  }

  if ((strnlen(argv[2], 2) == 1) && (argv[2][0] == '-')) {
    CrackPasswordsWithStdin(&userHashes);
  } else {
    CrackPasswords(&userHashes, string(argv[2]));
  }

  return 0;
}
