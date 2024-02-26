import ipih

from pih import A
from build_tools import build
from RecognizeService.const import SD

build(
    SD,
    requires_packages=(
        A.PTH_FCD_DIST.NAME(A.CT_SR.MOBILE_HELPER.standalone_name),
        A.PTH_FCD_DIST.NAME("tls"),
    ),
)
