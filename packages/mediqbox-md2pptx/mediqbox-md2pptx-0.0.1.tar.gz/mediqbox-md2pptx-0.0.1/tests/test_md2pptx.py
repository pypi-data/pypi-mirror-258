import os

from mediqbox.md2pptx import (
  Md2pptx,
  Md2pptxConfig,
  Md2pptxInputData
)

def test_md2pptx():
  working_dir = os.path.join(
    os.path.dirname(__file__),
    'data'
  )
  md_file = os.path.join(working_dir, 'Francesco.md')
  pptx_file = os.path.join(
    os.path.dirname(__file__),
    'test_results', 'Francesco.pptx'
  )

  md2pptx = Md2pptx(Md2pptxConfig())
  result = md2pptx.process(Md2pptxInputData(
    working_dir=working_dir, md_file=md_file, pptx_file=pptx_file
  ))

  assert result

if __name__ == '__main__':
  test_md2pptx()