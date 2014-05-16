// You can edit this code!
// Click here and start typing.
package main

import (
    "fmt"
    "os"
    "syscall"
    "encoding/json"
    "net/http"
    "path/filepath"
)

func findFile(poolID string, blockID string) string {
    prefix := "/mnt/var/lib/hadoop/dfs/current"
    basePath := fmt.Sprintf("%s/%s/current/finalized/blk_%s",
        prefix, poolID, blockID)
    _, err := os.Open(basePath)
    if err == nil {
        return basePath
    }
    subPath := fmt.Sprintf("%s/%s/current/finalized/*/blk_%s",
        prefix, poolID, blockID)
    matches, err := filepath.Glob(subPath)
    if err != nil {
        panic(err)
    }
    return matches[0]
}
func sumBytesHandler(w http.ResponseWriter, req *http.Request) {
    var request_map map[string]string
    dec := json.NewDecoder(req.Body)
    err := dec.Decode(&request_map)
    if err != nil {
        fmt.Fprintf(w, "Oh no, problem decoding!\n")
        return
    }
    filename := findFile(request_map["pool_id"], request_map["block_id"])
    buffer, _, err := GetFileBuffer(filename);
    if err != nil {
        fmt.Fprintf(w, "Oh no, %s doesn't exist!\n", filename)
        return
    }
    sum := sumBytes(buffer)
    fmt.Fprintf(w, "The sum is %d\n", sum)
}

func main() {
    fmt.Println("Listening on port 8080!")
    http.HandleFunc("/",sumBytesHandler)
    http.ListenAndServe(":8080", nil)
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
