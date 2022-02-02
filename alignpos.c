#include<stdlib.h>
#include<stdio.h>

/* main() returns int, not void. */
int main( void ) {

  int result ;
  result=system("python c:\\alignpos\\alignpos.pyw");
  printf("%d",result);
  return 0;
}