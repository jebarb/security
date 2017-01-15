#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "low_level_info.h"

int GetCurrentDirectoryContents(char **names, int max_files) {
  // Implementation goes here.
  char cwd[2048];
  DIR *dir;
  struct dirent *ent;
  int num_files;

  getcwd(cwd, sizeof(cwd));

  if ((dir = opendir(cwd)) == NULL)
    return EXIT_FAILURE;

  for (num_files = 0; (ent = readdir(dir)) != NULL && num_files < max_files; ++num_files) {
    names[num_files] = malloc(sizeof(ent->d_name));
    memcpy(names[num_files], ent->d_name, sizeof(ent->d_name));
  }

  closedir(dir);

  return num_files;
}
