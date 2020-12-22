/* The Computer Language Benchmarks Game
   http://benchmarksgame.alioth.debian.org/
   contributed by Isaac Gouy */

function TreeNode(left, right, item) {
  this.left = left;
  this.right = right;
  this.item = item;
}

TreeNode.prototype.itemCheck = function () {
  if (this.left == null) {
    return this.item;
  }
  else {
    return this.item + this.left.itemCheck() - this.right.itemCheck();
  }
};

function bottomUpTree(item, depth) {
  if (depth > 0) {
    return new TreeNode(
      bottomUpTree(2 * item - 1, depth - 1),
      bottomUpTree(2 * item, depth - 1),
      item
    );
  } else {
    return new TreeNode(null, null, item);
  }
}

const minDepth = 4;
const maxDepth = 15;
const stretchDepth = maxDepth + 1;

let check = bottomUpTree(0, stretchDepth).itemCheck();
console.log("stretch tree of depth " + stretchDepth + "\t check: " + check);

const longLivedTree = bottomUpTree(0, maxDepth);
for (let depth = minDepth; depth <= maxDepth; depth += 2) {
  const iterations = 1 << (maxDepth - depth + minDepth);

  check = 0;
  for (let i = 1; i <= iterations; i++) {
    check += bottomUpTree(i, depth).itemCheck();
    check += bottomUpTree(-i, depth).itemCheck();
  }
  console.log(iterations * 2 + "\t trees of depth " + depth + "\t check: " + check);
}

console.log(
  "long lived tree of depth " +
    maxDepth +
    "\t check: " +
    longLivedTree.itemCheck()
);
