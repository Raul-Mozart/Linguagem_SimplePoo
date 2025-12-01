@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00"

; ModuleID = 'SimplePOO'
target triple = "x86_64-pc-linux-gnu"

declare i32 @printf(i8*, ...)

define void @main() {
  entry:
    %0 = alloca i64
    store i64 18, i64* %0
    %1 = load i64, i64* %0
    %2 = icmp sge i64 %1, 18
    br i1 %2, label %if.then0, label %if.else1
  if.then0:
    %3 = getelementptr [4 x i8], [4 x i8]* @.str, i32 0, i32 0
    call i32 (i8*, ...) @printf(i8* %3, i64 1)
    br label %if.end2
  if.else1:
    %4 = getelementptr [4 x i8], [4 x i8]* @.str, i32 0, i32 0
    call i32 (i8*, ...) @printf(i8* %4, i64 0)
    br label %if.end2
  if.end2:
    ret void
}
