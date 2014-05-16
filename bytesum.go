// You can edit this code!
// Click here and start typing.
package main

import "fmt"
import "os"
import "syscall"

func main() {
    buffer, _, err := GetFileBuffer(os.Args[1]);
    if err != nil {
        panic(err)
    }
    result := sumBytes(buffer)
    fmt.Println(result)
}

func sumBytes(data []byte) uint8 {
    x := 0
    for b := range data {
        x += b
    }
    return uint8(x)
}

func GetFileBuffer(path string) ([]byte, int64, error) {
  f, err := os.Open(path)
  if err != nil {
    return nil, 0, err
  }
  fin, err := f.Stat()
  if err != nil {
    return nil, 0, err
  }

  mmap, err := syscall.Mmap(int(f.Fd()), 0, int(fin.Size()),
      syscall.PROT_READ, syscall.MAP_PRIVATE)
  if err != nil {
    return nil, 0, err
  }
  return mmap, fin.Size(), nil
}
