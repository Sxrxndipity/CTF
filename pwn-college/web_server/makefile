# Name of the target (without extension)
TARGET = test
OBJ = test.o

# Phony targets
.PHONY: all clean

# Default target
all: $(TARGET)

# Assemble the source file
$(OBJ): test.s
        as test.s -o $(OBJ)

# Link the object file to create the executable
$(TARGET): $(OBJ)
        ld $(OBJ) -o $(TARGET)

# Clean up the generated files
clean:
        rm -f $(TARGET) $(OBJ)
