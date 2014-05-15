// You can edit this code!
// Click here and start typing.
package main

import "bytes"
import "fmt"
import "os"
import "syscall"

func main() {
	fmt.Println("Hello, 世界")
    buffer, _, err := GetFileBuffer(os.Args[1]);
    if err != nil {
        panic(err)
    }
	fmt.Println(buffer)
}

func GetFileBuffer(path string) (*bytes.Buffer, int64, error) {
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
  buffer := bytes.NewBuffer(mmap)

  return buffer, fin.Size(), nil
}
