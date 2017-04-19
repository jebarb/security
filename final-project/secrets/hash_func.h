unsigned int hashPW(const std::string& username, const std::string& password) {
    const unsigned int A = 7;
    const unsigned int B = 5;
    
    const unsigned int FIRSTH = 37;

    std::string a = username + "::" + password;

    unsigned int h = FIRSTH;

    for(unsigned long i = 0; i < a.size(); i ++) {
        h = (h*A) ^ (((unsigned int)(a[i]))*B);
    }

    return h;
}
