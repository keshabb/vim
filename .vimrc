"https://realpython.com/vim-and-python-a-match-made-in-heaven/

set nocompatible
filetype off
set ruler
set title
set nu

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

" add all your plugins here (note older versions of Vundle
" used Bundle instead of Plugin)

" ...

Plugin 'vim-scripts/indentpython.vim'

set encoding=utf-8


map <leader>g  :YcmCompleter GoToDefinitionElseDeclaration<CR>

"https://github.com/tpope/vim-pathogen

execute pathogen#infect()

"https://github.com/vim-syntastic/syntastic

Plugin 'vim-syntastic/syntastic'

set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_python_checkers = ['pylint', 'flake8']
let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0

" https://github.com/nvie/vim-flake8
Plugin 'nvie/vim-flake8'

let python_highlight_all=1
syntax on

" https://github.com/jnurmine/Zenburn

"Plugin 'jnurmine/Zenburn'
"colors zenburn

" https://github.com/altercation/vim-colors-solarized
Plugin 'altercation/vim-colors-solarized'

"if has('gui_running')
"  set background=dark
"  colorscheme solarized
"endif

syntax enable
set background=light
let g:solarized_termcolors=256
colorscheme solarized

" https://github.com/ctrlpvim/ctrlp.vim
"https://github.com/kien/ctrlp.vim
Plugin 'kien/ctrlp.vim'
"Plugin 'ctrlpvim/ctrlp.vim'

"https://github.com/tpope/vim-fugitive
Plugin 'tpope/vim-fugitive'

"https://github.com/powerline/powerline
""https://powerline.readthedocs.io/en/latest/overview.html
Plugin 'Lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}
"Plugin 'powerline/powerline', {'rtp': 'powerline/bindings/vim/'}

set clipboard=unnamed

set backspace=indent,eol,start
Plugin 'davidhalter/jedi-vim'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

set splitbelow
set splitright

"split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>
