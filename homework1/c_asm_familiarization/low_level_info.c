#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include "low_level_info.h"

int GetCurrentDirectoryContents(char **names, int max_files) {
  // Implementation goes here.
  char cwd[2048];
  DIR *dir;
  struct dirent *ent;
  int num_files;

  // can use "." instead of getcwd()
  // get and open cwd, return errno on fail
  if (getcwd(cwd, sizeof(cwd)) == NULL || (dir = opendir(cwd)) == NULL)
    return errno;

  // for each file in cwd, malloc and copy name to names
  for (num_files = 0; (ent = readdir(dir)) != NULL && num_files < max_files; 
      ++num_files) {
    // can use strndup instead of malloc, memcpy
    // should be strlen, not sizeof
    if ((names[num_files] = malloc(sizeof(ent->d_name))) == NULL)
      return errno;
    memcpy(names[num_files], ent->d_name, sizeof(ent->d_name));
  }

  closedir(dir);

  return num_files;
}
