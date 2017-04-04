#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

/**********
 * NOTE: This file cannot be compiled in its current state.
 */

void handleErrors(void)
{
  ERR_print_errors_fp(stderr);
  abort();
}

int encrypt(unsigned char *plaintext, int plaintext_len, unsigned long unix_time,
    unsigned int pid, unsigned int nanosecond, unsigned char *ciphertext)
{
  EVP_CIPHER_CTX *ctx;

  int len, ciphertext_len;
  int i;

  // set random seed
  unsigned int utime = unix_time & 0xffffffff;
  srand(utime ^ pid ^ nanosecond);

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
