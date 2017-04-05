#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <ctype.h>

/**********
 * NOTE: This file cannot be compiled in its current state.
 */

void handleErrors(void)
{
  ERR_print_errors_fp(stderr);
  abort();
}

int encrypt(unsigned char *plaintext, int plaintext_len, unsigned long seed, unsigned char *ciphertext)
{
  EVP_CIPHER_CTX *ctx;

  int len, ciphertext_len;
  int i;

  // set random seed
  srand(seed);

  // create key and iv
  unsigned char key[32], iv[16];
  for (i = 0; i < 32; i++)
    key[i] = rand() & 0xff;
  for (i = 0; i < 16; i++)
    iv[i] = rand() & 0xff;

  /* Create and initialise the context */
  if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

  // AES 256, CTR mode
  if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_ctr(), NULL, key, iv))
    handleErrors();

  if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len))
    handleErrors();
  ciphertext_len = len;

  if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) handleErrors();
  ciphertext_len += len;

  /* Clean up */
  EVP_CIPHER_CTX_free(ctx);

  return ciphertext_len;
}

int check_if_ascii(unsigned char *plaintext, int plaintext_len) {
  while (plaintext_len-- > 0)
    if (isascii((int) *plaintext++)) return 1;
  return 0;
}

int main(int argc, char *argv[]) {
  int max_num = 65536;
  int utime_hi = 0;
  int utime_lo = 0;
  int utime = 0;
  unsigned char *plaintext;
  int plaintext_len;
  unsigned char *ciphertext;
  int ciphertext_len = 0;
  for (int hi = 0; hi + utime_hi < max_num && utime_hi - hi >= 0; ++hi) {
    for (int lo = 0; lo + utime_lo < max_num && utime_lo - lo >= 0; ++lo) {
      if (utime_hi + hi < max_num) {
        if (utime_lo + lo < max_num) {
          plaintext_len = encrypt(ciphertext, ciphertext_len, utime + hi + lo, plaintext);
          if (!check_if_ascii(plaintext, plaintext_len)) {
            fwrite(plaintext, plaintext_len, 1, stdout);
            return 0;
          }
        }
        if (utime_lo - lo > 0) {
          plaintext_len = encrypt(ciphertext, ciphertext_len, utime + hi - lo, plaintext);
          if (!check_if_ascii(plaintext, plaintext_len)) {
            fwrite(plaintext, plaintext_len, 1, stdout);
            return 0;
          }
        }
      }
      if (hi > 0 && utime_hi - hi > 0) {
        if (utime_lo + lo < max_num) {
          plaintext_len = encrypt(ciphertext, ciphertext_len, utime - hi + lo, plaintext);
          if (!check_if_ascii(plaintext, plaintext_len)) {
            fwrite(plaintext, plaintext_len, 1, stdout);
            return 0;
          }
        }
        if (utime_lo - lo > 0) {
          plaintext_len = encrypt(ciphertext, ciphertext_len, utime - hi - lo, plaintext);
          if (!check_if_ascii(plaintext, plaintext_len)) {
            fwrite(plaintext, plaintext_len, 1, stdout);
            return 0;
          }
        }
      }
    }
  }
  return 1;
}
