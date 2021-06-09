import math

if __name__ == "__main__":
  fp = open('text.docs', 'r')
  for row in fp:
    def calculate_entropy(values):
      if values == None:
        return 0

      e = 0
      for i in range(256):
        char = chr(i)

        temp = values.count(char) / len(values)
        if temp <= 0:
          pass
        else:
          temp_val = temp * math.log2(temp)
          temp_val = -temp_val
          e += temp_val

      return e
    print(calculate_entropy(row))
