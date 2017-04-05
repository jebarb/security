#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <ctype.h>
#include <string.h>

/**********
 * NOTE: This file cannot be compiled in its current state.
 */

void handleErrors(void)
{
  ERR_print_errors_fp(stderr);
  abort();
}

int decrypt(unsigned char *ciphertext, int ciphertext_len, unsigned char *key,
  unsigned char *iv, unsigned char *plaintext)
{
  EVP_CIPHER_CTX *ctx;

  int len;

  int plaintext_len;

  /* Create and initialise the context */
  if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

  /* Initialise the decryption operation. IMPORTANT - ensure you use a key
   * and IV size appropriate for your cipher
   * In this example we are using 256 bit AES (i.e. a 256 bit key). The
   * IV size for *most* modes is the same as the block size. For AES this
   * is 128 bits */
  if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_ctr(), NULL, key, iv))
    handleErrors();

  /* Provide the message to be decrypted, and obtain the plaintext output.
   * EVP_DecryptUpdate can be called multiple times if necessary
   */
  if(1 != EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len))
    handleErrors();
  plaintext_len = len;

  /* Finalise the decryption. Further plaintext bytes may be written at
   * this stage.
   */
  if(1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len)) handleErrors();
  plaintext_len += len;

  /* Clean up */
  EVP_CIPHER_CTX_free(ctx);

  return plaintext_len;
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

void get_key_iv(unsigned long seed, unsigned char *key, unsigned char *iv){
  // set random seed
  srand(seed);
  // create key and iv
  int i;
  for (i = 0; i < 32; i++)
    key[i] = rand() & 0xff;
  for (i = 0; i < 16; i++)
    iv[i] = rand() & 0xff;
}

int check_if_ascii(unsigned char *plaintext, int plaintext_len) {
  while (plaintext_len-- > 0)
    if (!isascii((int) *plaintext++)) return 0;
  return 1;
}

int force_decrypt(int utime_start, unsigned char *ciphertext, int ciphertext_len, unsigned char *plaintext){
  /*
    Starting at the given timestamp, 
    iterate in both directions MODIFYING LOW ORDER BITS FIRST
  */
  unsigned int utime_upper = utime_start & 0xffff0000; // Mask off lower 16
  unsigned int utime_inc_value = 0x00010000; // 2^16
  unsigned int utime_plus = utime_upper;
  unsigned int utime_minus = utime_upper - utime_inc_value;
  unsigned int plaintext_len;
  unsigned char key[32], iv[16];
  
  while (1){
    // iterate over lower bits
    for (unsigned int lower_bits = 0; lower_bits <= 0xffff; lower_bits++){
      if (utime_plus){
        unsigned long seed = (unsigned long) (utime_plus | lower_bits) ;
        get_key_iv(seed, key, iv);
        // printf("%lu, %d, %d, %d, %s\n", seed, utime_plus, lower_bits, iv, plaintext);
        plaintext_len = decrypt(ciphertext, ciphertext_len, key, iv, plaintext);
        if (check_if_ascii(plaintext, plaintext_len))
          return plaintext_len;        
      }
      if (utime_minus){
        get_key_iv((unsigned long) utime_minus & lower_bits, &key, &iv);
        plaintext_len = decrypt(ciphertext, ciphertext_len, key, iv, plaintext);
        if (check_if_ascii(plaintext, plaintext_len))
          return plaintext_len;     
      }
    }

    if (utime_plus)
      utime_plus += utime_inc_value;
    if (utime_minus)
      utime_minus -= utime_inc_value; 
    if (utime_minus && utime_plus){
      printf("FAILED\n");
      break; // NO KEY EXISTS
    }
  }
}

int main(int argc, char *argv[]) {

  unsigned char *plaintext = (unsigned char*)"THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
  unsigned int plaintext_len = 43;

  unsigned char *ciphertext = malloc(sizeof(unsigned char) * plaintext_len);
  //unsigned char *plaintext, int plaintext_len, unsigned long seed, unsigned char *ciphertext
  unsigned int ciphertext_len = encrypt(plaintext, plaintext_len, (unsigned long) 0x12345678, ciphertext);
  printf("%d\n", ciphertext_len);

  unsigned char* unencrypted = malloc(sizeof(unsigned char)*ciphertext_len);
  force_decrypt(0x12340000, ciphertext, ciphertext_len, unencrypted);
  printf("%s\n", unencrypted);
  return 0;
}
