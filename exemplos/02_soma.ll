@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00"

; ModuleID = 'SimplePOO'
target triple = "x86_64-pc-linux-gnu"

declare i32 @printf(i8*, ...)

define void @main() {
  entry:
    %0 = alloca i64
    store i64 10, i64* %0
    %1 = alloca i64
    store i64 20, i64* %1
    %2 = alloca i64
    %3 = load i64, i64* %0
    %4 = load i64, i64* %1
    %5 = add i64 %3, %4
    store i64 %5, i64* %2
    %6 = load i64, i64* %2
    %7 = getelementptr [4 x i8], [4 x i8]* @.str, i32 0, i32 0
    call i32 (i8*, ...) @printf(i8* %7, i64 %6)
    ret void
}
