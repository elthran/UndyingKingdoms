// you don't need to use these, just put all chunked files in here.
// NOTE: chunking only works if the component that usese them is also async

// These chunks are for ChatRoom -> vue-markdown
const unorm = () => import(/* webpackChunkName: "unorm" */ 'unorm')
const uslug = () => import(/* webpackChunkName: "uslug" */ 'uslug')
const katex = () => import(/* webpackChunkName: "katex" */ 'katex')
